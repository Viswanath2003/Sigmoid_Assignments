from flask import Flask, render_template, request, redirect, url_for, flash, session
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = "supersecret"

# Initialize S3 client
s3 = boto3.client("s3")



# List all buckets (Landing page)

@app.route("/")
def list_buckets():
    response = s3.list_buckets()
    buckets = response.get("Buckets", [])
    return render_template("bucket.html", buckets=buckets)


# View bucket contents (objects + folders)

@app.route("/bucket/<bucket_name>/")
@app.route("/bucket/<bucket_name>/<path:prefix>")
def view_bucket(bucket_name, prefix=""):
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter="/"
    )

    folders = response.get("CommonPrefixes", [])
    objects = response.get("Contents", [])
    if objects:
        objects = [f for f in objects if f["Key"] != prefix]

    breadcrumb = []
    if prefix:
        parts = prefix.strip("/").split("/")
        for i, part in enumerate(parts):
            path = "/".join(parts[:i+1]) + "/"
            breadcrumb.append({"name": part, "path": path})
    
    return render_template(
        "index.html",
        bucket_name=bucket_name,
        prefix=prefix,
        folders=folders,
        objects=objects,
        breadcrumb=breadcrumb
    )


# Upload file to S3

@app.route("/upload/<bucket_name>/", defaults={"prefix": ""}, methods=["POST"])
@app.route("/upload/<bucket_name>/<path:prefix>", methods=["POST"])
def upload_file(bucket_name, prefix=""):
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

    key = prefix + file.filename
    try:
        s3.upload_fileobj(file, bucket_name, key)
        flash(f"Uploaded {file.filename} to {bucket_name}/{prefix}")
    except Exception as e:
        flash(f"Upload failed: {str(e)}")

    return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

# Delete file
@app.route("/delete/<bucket_name>/<path:key>", methods=["POST"])
def delete_file(bucket_name, key):
    try:
        s3.delete_object(Bucket=bucket_name, Key=key)
        flash(f"Deleted {key} from {bucket_name}")
    except Exception as e:
        flash(f"Delete failed: {str(e)}")
    prefix = "/".join(key.split("/")[:-1]) + "/"
    return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

# Create folder
@app.route("/create_folder/<bucket_name>/", defaults={"prefix": ""}, methods=["POST"])
@app.route("/create_folder/<bucket_name>/<path:prefix>", methods=["POST"])
def create_folder(bucket_name, prefix=""):
    folder_name = request.form.get("folder_name", "").strip()
    if not folder_name:
        flash("Folder name cannot be empty")
        return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

    folder_key = prefix + folder_name + "/"
    try:
        s3.put_object(Bucket=bucket_name, Key=folder_key)
        flash(f"Folder '{folder_name}' created successfully in {bucket_name}/{prefix}")
    except Exception as e:
        flash(f"Failed to create folder: {str(e)}")

    return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

# Delete folder (+contents)
@app.route("/delete_folder/<bucket_name>/<path:folder_key>", methods=["POST"])
def delete_folder(bucket_name, folder_key):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_key)
        objects_to_delete = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
        if objects_to_delete:
            s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects_to_delete})
        flash(f"Folder '{folder_key}' and its contents deleted successfully from {bucket_name}")
    except Exception as e:
        flash(f"Delete folder failed: {str(e)}")

    parent_prefix = "/".join(folder_key.strip("/").split("/")[:-1])
    if parent_prefix:
        parent_prefix += "/"
    return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=parent_prefix))

# Download file
@app.route("/download/<bucket_name>/<path:key>")
def download_file(bucket_name, key):
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=60
        )
        return redirect(url)
    except Exception as e:
        flash(f"Download failed: {str(e)}")
        prefix = "/".join(key.split("/")[:-1])
        return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

# Create a new bucket
@app.route("/create_bucket", methods=["POST"])
def create_bucket():
    bucket_name = request.form.get("bucket_name")
    if not bucket_name:
        flash("Bucket name cannot be empty", "danger")
        return redirect(url_for("list_buckets"))

    existing_buckets = [b['Name'] for b in s3.list_buckets().get('Buckets', [])]
    if bucket_name in existing_buckets:
        flash(f"Bucket '{bucket_name}' already exists", "danger")
        return redirect(url_for("list_buckets"))

    try:
        region = s3.meta.region_name
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        flash(f"Bucket '{bucket_name}' created successfully!", "success")
    except ClientError as e:
        flash(f"Bucket creation failed: {e.response['Error']['Message']}", "danger")
    except Exception as e:
        flash(f"Bucket creation failed: {str(e)}", "danger")

    return redirect(url_for("list_buckets"))

#Delete Bucket
@app.route("/delete_bucket/<bucket_name>", methods=["POST"])
def delete_bucket(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get("Contents", [])
        if objects:
            delete_keys = [{'Key': obj['Key']} for obj in objects]
            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})
        s3.delete_bucket(Bucket=bucket_name)
        flash(f"Bucket '{bucket_name}' deleted successfully!", "success")
    except Exception as e:
        flash(f"Failed to delete bucket '{bucket_name}': {str(e)}", "danger")
    return redirect(url_for("list_buckets"))

#Copy/Move

@app.route("/set_action/<action>/<bucket_name>/<path:key>")
def set_action(action, bucket_name, key):
    """User clicked Copy or Move on a file: remember what to do and from where."""
    if action not in ["copy", "move"]:
        flash("Invalid action", "danger")
        # safe fallback to the file's parent folder
        parent_prefix = "/".join(key.split("/")[:-1])
        if parent_prefix:
            parent_prefix += "/"
        return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=parent_prefix))

    session["source_bucket"] = bucket_name
    session["source_key"] = key
    session["action"] = action

    flash(f"{action.capitalize()} selected: {key}", "info")
    # Prefer referrer; fall back to parent folder listing
    if request.referrer:
        return redirect(request.referrer)
    parent_prefix = "/".join(key.split("/")[:-1])
    if parent_prefix:
        parent_prefix += "/"
    return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=parent_prefix))

@app.route("/copy_file_here/<bucket_name>/", defaults={"prefix": ""}, methods=["POST"])
@app.route("/copy_file_here/<bucket_name>/<path:prefix>", methods=["POST"])
def copy_file_here(bucket_name, prefix):
    """User clicked 'Copy/Move Here' in the destination. Do copy or move based on session."""
    source_bucket = session.get("source_bucket")
    source_key = session.get("source_key")
    action = session.get("action")

    if not source_bucket or not source_key or not action:
        flash("Please select a file to copy or move first", "warning")
        return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))

    # normalize prefix
    if prefix and not prefix.endswith("/"):
        prefix += "/"

    destination_key = f"{prefix}{source_key.split('/')[-1]}"

    try:
        # 1) Copy
        s3.copy_object(
            Bucket=bucket_name,
            CopySource={"Bucket": source_bucket, "Key": source_key},
            Key=destination_key,
        )

        # 2) Move
        if action == "move":
            s3.delete_object(Bucket=source_bucket, Key=source_key)
            flash(f"Moved {source_bucket}/{source_key} → {bucket_name}/{destination_key}", "success")
        else:
            flash(f"Copied {source_bucket}/{source_key} → {bucket_name}/{destination_key}", "success")

        # Clear session
        session.pop("source_bucket", None)
        session.pop("source_key", None)
        session.pop("action", None)

    except Exception as e:
        flash(f"Error during {action}: {e}", "danger")

    return redirect(url_for("view_bucket", bucket_name=bucket_name, prefix=prefix))


if __name__ == "__main__":
    app.run(debug=True)
