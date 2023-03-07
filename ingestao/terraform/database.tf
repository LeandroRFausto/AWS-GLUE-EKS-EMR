resource "aws_db_instance" "default" {
  allocated_storage      = 10
  engine                 = "mysql"
  engine_version         = "8.0.28"
  instance_class         = "db.t2.micro"
  db_name                = "lrfawsmysql"
  username               = var.username
  password               = var.password
  db_subnet_group_name   = aws_db_subnet_group.education.name
  vpc_security_group_ids = [aws_security_group.allow_mysql.id]
  skip_final_snapshot    = true
  multi_az               = false
  identifier             = "${var.prefix}-learning-db-mysql-${var.account_id}"
  publicly_accessible    = true
}