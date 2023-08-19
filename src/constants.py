import os

URL_TO_SHEETS = "https://docs.google.com/spreadsheets/d/1up6bYQj2X5XoYfS9aN8zAT5oz8dFQIGZlXCr_Madgug/edit#gid=1700410190"
INDEXING_SEARCH_STRING = "https://www.google.com/search?q=site:{}&num=1"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
}
SERVICE_ACCOUNT = {
    "type": "service_account",
    "project_id": "email-395608",
    "private_key_id": "991d8f3b50f01597c111232877f7434ed0866e3d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfE9ZSrWqGeq2o\n4uJhQQk5rwEsANBn6/SKA59CIEfEi8+Mc2KYp+a0JgKF28A/oItDaRxwofmn/y0d\njuXSueqf1IAUCGh928YJ/KOMEMsl5HvMdYy/8vAzwO2A4RAuoa5wKy6TSM7BmlF3\n+lsKz2d/M7c3DvobsoqWp+XX/pz91BkbTjNH5UCJh9aDIcnSji3U7gXjM+UJ/tw9\nW7tAroInlZ/8ssg1s/4oJBO2OH2sL1ekPtQ7e4anRY++pn1Fh/Girh5xmj2BBo0P\nwQEiEWHp6d7D8nD4C5fUUJ145rM7Bj+ycVYQxNQJY4Cq/GFk4Y8zhVrcVMnsqEVS\nqgMA5YGlAgMBAAECggEAJ6ES/vTJuWe9dHnVKKJBkJe65IHtaT48ZNeDKL+O8XVd\nBqHGGb6WOCHR9hPpIFC38NqyJZMMdWAaFqd/NJBxVVDkeVkg4t3Jx7oi6iVS3oU9\nnBFat4TndxUkdbtbwyovIS14xGNacpulmQyK+rXxlBxHk9VM1HKVmPOJzFXXOVpl\nOEy3gRPVKaMxc8+wo/D2M/bYx4dozc7YaUJ3Goqrzx0+MLOU0lqSkVHpXI7hRtbh\n6rNzd8bwg4naWMi1FRaJA1gb417mnOPaVzixRNGMdxntfodUNlSpPRcWJxp4pAQN\nEawfgj8I7W47xsnGr8PrL4uAwSRnQOMm6GFrkI1t3wKBgQDNolaP0w2w9X7byqt3\nUEiyK+NAF8j6oTywNRQizTAV8qlHZK3y2lzMH4HLWoKMOtggs7t0Whm0XbqDFcyH\nqgsq+A+uLMlVEL6LAV+ZjpjYln1J8YlffZ2WKkIzJC9OKTNCfHA38n0tYzL3u1YC\nBM7xxYFdv5aq0bglTewYk657cwKBgQDGCk54QNmAXHulYcXeKzjdv3a3zVfj/B33\noMcZjXSmBbm753cf8p2HieJ9UWm5oFDIIqDtwe/wzw2IWW5jfwi+A1OmJU1wY0Jy\nIseZbjfMBsAffyz+isczhdiU/kk/IcqRTioOLHo7ZfgxfP8nPXkbtZ2P5AiKYih9\nepR5acn4hwKBgG5aKh3w4y4N8NA+yRm0ie6jwsaIfSCTGqBtO6sZdi6xFMrtarQj\nHx2j4uGgZuKeSZHzIivkllrG2eqy7hn31RpwGOodusXdwIOUbxtW/QtuZzohVtlZ\n7hHCB9iuGHzXe1y4rvg3N5n93EI51IQs1GnG1g/bWx28ghfy4zqlNkOlAoGAODiC\n0FawqGUY4Plhv9GLYkBRhppv4hQXuc3V1+Y1gFBNyw9J3TL2D51QQ/1Rw1XEuRxD\njVuqLzXIhLXGxc4xgCfXnmomkspK+bXv7hnBE1WzQv3KmzRwmqrbsmiCCL8iD6Ae\nBkoQJT6sd/ghQ1WLRReI9GlrF0YIcp7S+ajToo8CgYEAhkWmXx4D0j6EeZBCH/d5\nlMq3C0XpmGVkJ0MEMCbIBsRMlVv7U4/EqagIldpwA/Wb1CtJLDj0G7lOB53yQb4g\n+ASREAu8EBa8iSESXAAGBlNe4rrC3eToaTlhi6cm19IKNEimWzdS1FzFDYoAdqa2\nWdadFvXi6gdP30A1VMhlYTA=\n-----END PRIVATE KEY-----\n",
    "client_email": "sitecheck@email-395608.iam.gserviceaccount.com",
    "client_id": "103213817168363782595",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sitecheck%40email-395608.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}
