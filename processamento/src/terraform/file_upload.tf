resource "aws_s3_object" "jars" {
  bucket = "lrfaws-scripts-dev-521738873930"
  key    = "jars/delta-core_2.12-1.0.0.jar"
  source = "../jars/delta-core_2.12-1.0.0.jar"
  etag   = filemd5("../jars/delta-core_2.12-1.0.0.jar")
}

resource "aws_s3_object" "class" {
  bucket = "lrfaws-scripts-dev-521738873930"
  key    = "job/DeltaProcessing.py"
  source = "../job/DeltaProcessing.py"
  etag   = filemd5("../job/DeltaProcessing.py")
}

resource "aws_s3_object" "etl" {
  bucket = "lrfaws-scripts-dev-521738873930"
  key    = "job/etl.py"
  source = "../job/etl.py"
  etag   = filemd5("../job/etl.py")
}

resource "aws_s3_object" "variables" {
  bucket = "lrfaws-scripts-dev-521738873930"
  key    = "job/variables.py"
  source = "../job/variables.py"
  etag   = filemd5("../job/variables.py")
}


