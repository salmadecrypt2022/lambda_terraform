resource "aws_s3_bucket" "b" {
  bucket = "issuance-terraform-websites"
  
  

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.b.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


  

resource "aws_s3_bucket_acl" "example1" {
  bucket = aws_s3_bucket.b.id
  acl    = "public-read"
}
resource "aws_s3_bucket_object" "object" {
  bucket = aws_s3_bucket.b.id
  key    = ""
  source = ""
}

resource "aws_lambda_permission" "test" {
statement_id  = "AllowS3Invoke"
action        = "lambda:InvokeFunction"
function_name = "${aws_lambda_function.terraform_lambda_func.id}"
principal = "s3.amazonaws.com"
source_arn = "arn:aws:s3:::${aws_s3_bucket.b.id}"

}
