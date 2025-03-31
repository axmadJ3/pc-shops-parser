JAZZMIN_SETTINGS = {
    "site_title": "it.next Admin",
    "site_header": "it.next",
    "site_brand": "dmin panel",
    "login_logo": "images/logos/it_logo.png",
    "welcome_sign": "it.next Admin paneliga xush kelibsiz",
    "copyright": "Timur, IT.NEXT Ltd",
    "user_avatar": None,
    "theme": "flatly",

    "topmenu_links": [
        {"name": "Bosh sahifa",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Veb sahifa", "url": "http://127.0.0.1:8000", "new_window": True},
    ],
    "search_model": "main.Product",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["main", "main.Product", "auth.user"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,

    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "theme": "default",
    "sidebar_nav_small_text": False,
    "sidebar_fixed": True,
}
