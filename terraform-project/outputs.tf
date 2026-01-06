output "public_instance_ip" {
  value = module.ec2.public_ip
}

output "nginx_url" {
  value = "http://${module.ec2.public_ip}"
}
