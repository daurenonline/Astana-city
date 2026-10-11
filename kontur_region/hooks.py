app_name = "kontur_region"
app_title = "Контур региона"
app_publisher = "Dauren Bolatov"
app_description = "Единая система оперативного контроля сроков инфраструктурных проектов региона (GTON 2026)"
app_email = "bolatov.db@gmail.com"
app_license = "MIT"

# Apps
# ------------------
# required_apps = []

# Each item in the list will be shown as an app in the desk
# add_to_apps_screen = [
# 	{
# 		"name": "kontur_region",
# 		"logo": "/assets/kontur_region/logo.png",
# 		"title": "Контур региона",
# 		"route": "/app/infrastructure-object"
# 	}
# ]

# Includes in <head>
# ------------------
# app_include_css = "/assets/kontur_region/css/kontur.css"
# app_include_js = "/assets/kontur_region/js/kontur.js"

# Scheduled Tasks
# ------------------
scheduler_events = {
    # Daily cron to compute overdue flags across all infrastructure objects
    "daily": [
        "kontur_region.tasks.recalculate_all_overdue"
    ]
}

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "Infrastructure Object": {
        "validate": "kontur_region.doctype.infrastructure_object.infrastructure_object.validate_deadline",
        "on_update": "kontur_region.doctype.infrastructure_object.infrastructure_object.on_object_update"
    }
}

# Website Routing
# ---------------
website_route_rules = [
    {"from_route": "/kontur", "to_route": "kontur"},
    {"from_route": "/presentation", "to_route": "presentation"}
]
