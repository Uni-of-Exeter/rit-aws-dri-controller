resource "aws_s3_bucket" "data" {
  bucket = "${var.environment}-${var.name}"
}
