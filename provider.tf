terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.36.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-west-2"
}
resource "aws_iam_role" "lambda_role" {
  name = "terraform_aws_lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
        
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
resource "aws_iam_policy" "iam_policy_for_lambda" {
  name = "aws_iam_policy_for_terraform_aws_lambda_role"
  path = "/"
  description = "AWS IAM Policy for managing aws lambda role"

  policy =  jsonencode({

  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
         "s3:GetObject",
         "s3:GetObjectVersion",
         "s3:ListBucket",
         "s3:*",
         "s3-object-lambda:*",
         "ec2:*",
         "ec2:Describe*"
         
         
      ],
      "Effect": "Allow",
      "Resource": "*"
      
      
    }
  ]
})
}



resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role"{
  role = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn

}
data "archive_file" "zip_the_python_code" {
  type = "zip"
  source_dir = "${path.module}/python/"
  output_path = "${path.module}/python/hello.python.zip"

}
 resource "aws_lambda_function" "terraform_lambda_func"{
  filename = "${path.module}/python/hello.python.zip"
  function_name = "Terraform-Lambda-Function"
  role = aws_iam_role.lambda_role.arn
  handler = "hello-python.lambda_handler"
  runtime = "python3.9"
  depends_on =  [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
  timeouts {
    create= "1m"
  }
 }
 output "terraform_aws_role_output" {
  value = aws_iam_role.lambda_role.name
 }
 output "terraform_aws_role_arn_output" {
  value = aws_iam_role.lambda_role.arn
 }
 output "terraform_logging_arn_output" {
  value = aws_iam_policy.iam_policy_for_lambda.arn
 }
   
 
  
