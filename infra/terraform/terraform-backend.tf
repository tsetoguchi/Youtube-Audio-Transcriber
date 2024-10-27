provider "aws" {}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "metabucket-tf"
    key            = "youtube-audio-transcriber/shaafe.tfstate"
    dynamodb_table = "terraform-state-lock"
    region         = "eu-west-1"
  }
}