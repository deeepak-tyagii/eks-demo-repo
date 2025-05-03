terraform {
  backend "s3" {
    bucket         = "terraform-state-file-dt"
    key            = "test/aws_infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
} 