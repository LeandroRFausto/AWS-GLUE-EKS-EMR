resource "aws_glue_crawler" "crawler" {
  database_name = "lrfaws-database"
  name          = "lrfaws-crawler"
  role          = aws_iam_role.glue_job.arn

  delta_target {
    connection_name = aws_glue_connection.delta_connection.name
    delta_tables = [
      "s3://lrfaws-silver-layer-dev-521738873930/delivery/customers/", 
      "s3://lrfaws-silver-layer-dev-521738873930/delivery/credit_score/", 
      "s3://lrfaws-silver-layer-dev-521738873930/delivery/music/" 
    ]
    write_manifest = "true"
  }
}

resource "aws_glue_connection" "delta_connection" {
  name = "delta_connection"
  connection_type = "NETWORK"

    physical_connection_requirements {
      availability_zone      = "us-east-2a"
      security_group_id_list = ["sg-02a799edc257f64c0"]
      subnet_id              = "subnet-0bece10902440b3c7"
    }
}