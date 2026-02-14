output "ecs_cluster_name" {
  value = aws_ecs_cluster.agent_cluster.name
}

output "postgres_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "mongodb_endpoint" {
  value = aws_docdb_cluster.mongodb.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}
