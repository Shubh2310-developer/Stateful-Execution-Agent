provider "aws" {
  region = var.aws_region
}

# ECS Cluster for the Agent
resource "aws_ecs_cluster" "agent_cluster" {
  name = "${var.app_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS instance for PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier           = "${var.app_name}-db"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.micro"
  db_name              = "stateful_agent_data"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
}

# DocumentDB for MongoDB (State)
resource "aws_docdb_cluster" "mongodb" {
  cluster_identifier      = "${var.app_name}-state"
  engine                  = "docdb"
  master_username         = var.db_username
  master_password         = var.db_password
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
  skip_final_snapshot     = true
}

# ElastiCache for Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${var.app_name}-cache"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}
