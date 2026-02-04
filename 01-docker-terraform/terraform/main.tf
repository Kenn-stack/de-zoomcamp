terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = "de-zoomcamp-483921"
  region  = "us-central1"

}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "de-zoomcamp-483921-terra-bucket"
  location      = "us-central1"

  # Optional, but recommended settings:
  storage_class = "REGIONAL"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "AbortIncompleteMultipartUpload"
    }
    condition {
      age = 1
    }
  }
  force_destroy = true
}
