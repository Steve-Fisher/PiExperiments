# Steps to set up logging of temp data to Azure Storage

## Azure Storage set up
```json
{
    "sku": {
        "name": "Standard_LRS",
        "tier": "Standard"
    },
    "kind": "StorageV2",
    "id": "/subscriptions/a8814926-bc3b-4b67-904e-d3fc5fc50112/resourceGroups/Logging-rg/providers/Microsoft.Storage/storageAccounts/versibleloggingstorage",
    "name": "versibleloggingstorage",
    "type": "Microsoft.Storage/storageAccounts",
    "location": "westeurope",
    "tags": {},
    "properties": {
        "dnsEndpointType": "Standard",
        "defaultToOAuthAuthentication": false,
        "publicNetworkAccess": "Enabled",
        "keyCreationTime": {
            "key1": "2023-05-12T20:16:40.0805770Z",
            "key2": "2023-05-12T20:16:40.0805770Z"
        },
        "allowCrossTenantReplication": false,
        "privateEndpointConnections": [],
        "isSftpEnabled": false,
        "minimumTlsVersion": "TLS1_2",
        "allowBlobPublicAccess": true,
        "allowSharedKeyAccess": true,
        "isHnsEnabled": true,
        "networkAcls": {
            "resourceAccessRules": [],
            "bypass": "AzureServices",
            "virtualNetworkRules": [],
            "ipRules": [
                {
                    "value": "212.159.102.76",
                    "action": "Allow"
                }
            ],
            "defaultAction": "Deny"
        },
        "supportsHttpsTrafficOnly": true,
        "encryption": {
            "requireInfrastructureEncryption": false,
            "services": {
                "file": {
                    "keyType": "Account",
                    "enabled": true,
                    "lastEnabledTime": "2023-05-12T20:16:40.3774909Z"
                },
                "blob": {
                    "keyType": "Account",
                    "enabled": true,
                    "lastEnabledTime": "2023-05-12T20:16:40.3774909Z"
                }
            },
            "keySource": "Microsoft.Storage"
        },
        "accessTier": "Hot",
        "provisioningState": "Succeeded",
        "creationTime": "2023-05-12T20:16:39.9399473Z",
        "primaryEndpoints": {
            "dfs": "https://versibleloggingstorage.dfs.core.windows.net/",
            "web": "https://versibleloggingstorage.z6.web.core.windows.net/",
            "blob": "https://versibleloggingstorage.blob.core.windows.net/",
            "queue": "https://versibleloggingstorage.queue.core.windows.net/",
            "table": "https://versibleloggingstorage.table.core.windows.net/",
            "file": "https://versibleloggingstorage.file.core.windows.net/"
        },
        "primaryLocation": "westeurope",
        "statusOfPrimary": "available"
    }
```

## Command to upload to Azure Storage
```bash
az storage blob upload -f "c:\users\steve\Hello World.txt" -c atc-templog -n HelloWorld4.txt --account-name versibleloggingstorage --account-key OnN796gggyWZhzxvoKjJiLX/5DnNY2SUPWvVp856QqdCybt14sWd1L5gvzNd1mcWtvFH4qs4qigk+ASt7iIvxg==
```