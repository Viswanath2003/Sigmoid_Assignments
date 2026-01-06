resource "aws_security_group" "public_sg" {
  name   = "public-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "public_vm" {
  ami                    = "ami-0e2c8caa4b6378d8c" # Amazon Linux 2 (us-east-1)
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  key_name               = var.key_name
  security_groups        = [aws_security_group.public_sg.id]
  associate_public_ip_address = true

  user_data = <<EOF
#!/bin/bash
yum install -y nginx
systemctl enable nginx
systemctl start nginx
EOF
}

resource "aws_instance" "private_vm" {
  ami                    = "ami-0e2c8caa4b6378d8c"
  instance_type          = var.instance_type
  subnet_id              = var.private_subnet_id
  key_name               = var.key_name
  associate_public_ip_address = false
}

output "public_ip" {
  value = aws_instance.public_vm.public_ip
}
