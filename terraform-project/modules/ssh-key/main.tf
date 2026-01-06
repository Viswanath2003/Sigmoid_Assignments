resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated" {
  key_name   = "terraform_key"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

resource "local_file" "private_key" {
  filename = "terraform_key.pem"
  content  = tls_private_key.ssh_key.private_key_pem
}

output "key_name" {
  value = aws_key_pair.generated.key_name
}
