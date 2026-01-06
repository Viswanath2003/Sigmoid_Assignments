module "networking" {
  source              = "./modules/networking"
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
}

module "ssh_key" {
  source = "./modules/ssh-key"
}

module "ec2" {
  source               = "./modules/ec2"
  public_subnet_id     = module.networking.public_subnet_id
  private_subnet_id    = module.networking.private_subnet_id
  vpc_id               = module.networking.vpc_id
  key_name             = module.ssh_key.key_name
  instance_type        = var.instance_type
}
