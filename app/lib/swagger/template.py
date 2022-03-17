template = {
    "swagger": "2.0",
    "info": {
        "title": "Naive Bayes Beasiswa API",
        "description": "pengambilan keputusan penerimaan beasiswa",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "deve@gmail.com",
            "url": "www.twitter.com/deve",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}
