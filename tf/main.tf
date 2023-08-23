resource "elephantsql_instance" "sql_fruity" {
  name="Fruity"
  plan="turtle"
  region="amazon-web-services::sa-east-1"
}

output "db_url" {
  value = elephantsql_instance.sql_fruity.url
  sensitive = true
}