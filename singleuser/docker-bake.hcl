// Define variables for reuse
variable "REGISTRY" {
    default = "lcas.lincoln.ac.uk"
}

variable "OWNER" {
    default = "lcas"
}

// Base group for common settings
group "default" {
    targets = ["jupyter-singleuser"]
}

// Target definition for jupyter-singleuser
target "jupyter-singleuser" {
    context = "."
    dockerfile = "Dockerfile"
    tags = [
        "${REGISTRY}/${OWNER}/jupyter_singleuser:latest"
    ]
    platforms = ["linux/amd64"]
}