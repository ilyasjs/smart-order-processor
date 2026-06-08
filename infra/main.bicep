param storageAccountName string = 'orderprocessor'
param location string = 'swedencentral'
param serviceBusName string = 'smart-order-processor-sb'
param appServicePlanName string = 'smart-order-processor-plan'
param functionAppName string = 'smart-order-processor-func'
param databaseAccountName string = 'smart-order-processor-db'
param ordersDatabaseName string = 'orders-db'
param ordersContainerName string = 'orders'



resource storageAccount 'Microsoft.Storage/storageAccounts@2024-01-01' = {
    name: storageAccountName
    location: location
    sku: {
        name: 'Standard_LRS'
    }
    kind: 'StorageV2'
    properties: {
        accessTier: 'Hot'
    }
}

resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2024-01-01' = {
    name: serviceBusName
    location: location
    sku: {
        name: 'Standard'
        tier: 'Standard'
    }
}

resource serviceBusQueue 'Microsoft.ServiceBus/namespaces/queues@2024-01-01' = {
    parent: serviceBusNamespace
    name: 'orders-queue'
    properties: {
        lockDuration: 'PT30S'
        maxDeliveryCount: 10
        deadLetteringOnMessageExpiration: true
    }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {
    name: appServicePlanName
    location: location
    kind: 'functionapp'
    sku: {
        name: 'Y1'
        tier: 'Dynamic'
    }
}

resource functionApp 'Microsoft.Web/sites@2024-04-01' = {
    name: functionAppName
    location: location
    kind: 'functionapp'
    properties:{
        serverFarmId: appServicePlan.id
        siteConfig: {
            pythonVersion: '3.11'
        }
    }
}

resource databaseAccount 'Microsoft.DocumentDB/databaseAccounts@2024-11-15' = {
    name: databaseAccountName
    location: location
    kind: 'GlobalDocumentDB'
    properties: {
        databaseAccountOfferType: 'Standard'
        locations: [
            {
                locationName: location
                failoverPriority: 0
                isZoneRedundant: false
            }
        ]
    }
}

resource ordersDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-11-15' = {
    parent: databaseAccount
    name: ordersDatabaseName
    properties: {
        resource: {
            id: ordersDatabaseName
        }
    }
}

resource ordersContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-11-15' = {
    parent: ordersDatabase
    name: ordersContainerName
    properties: {
        resource: {
            id: ordersContainerName
            partitionKey: {
                kind: 'Hash'
                paths: ['/orderId']}
        }
    
    }
}


    