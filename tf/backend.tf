terraform {
  required_providers {
    elephantsql = {
      source = "elephantsql/elephantsql"
    }
  }
  cloud {
    organization = "MatTerra"

    workspaces {
      name = "Fruity"
    }
  }
}