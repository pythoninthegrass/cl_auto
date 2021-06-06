provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

resource "kubernetes_secret" "jss_migrator" {
  metadata {
    name = "jss-migrator"
  }
    data = {
    EC2_KEY = ""
    K8S_KEY = ""
  }
  lifecycle {
      ignore_changes=[
          data
      ]
  }
}

resource "kubernetes_cron_job" "jss_migrator" {
  metadata {
    name = "jss-migrator"
  }
  spec {
    concurrency_policy            = "Replace"
    failed_jobs_history_limit     = 5
    schedule                      = "* * * * *"
    starting_deadline_seconds     = 10
    successful_jobs_history_limit = 5
    job_template {
      metadata {
          labels = {
            "job-template-label" = "value"
          }
      }
      spec {
        backoff_limit              = 2
        ttl_seconds_after_finished = 10
        template {
          metadata {
              labels = {
                "spec-template-label" = "value"
              }
          }
          spec {
            container {
              name    = "python-code"
              image   = "runner"
              image_pull_policy = "Never"
              env {
                name = "EC2_KEY"
                value_from {
                    secret_key_ref {
                        key = "EC2_KEY"
                        name = "jss-migrator"
                    }
                }
              }
              env {
                name = "K8S_KEY"
                value_from {
                    secret_key_ref {
                        key = "K8S_KEY"
                        name = "jss-migrator"
                    }
                }
              }
            #   command = ["/bin/sh", "-c", "date; echo Hello from the Kubernetes cluster"]
            }
          }
        }
      }
    }
  }
}
