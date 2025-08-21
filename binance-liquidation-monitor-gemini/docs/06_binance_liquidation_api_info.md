# Binance Liquidation Order Streams API Information

**Stream Name:** `<symbol>@forceOrder`

**Update Speed:** 1000ms

**Response Example:**
```json
{
    "e":"forceOrder",                // Event Type
    "E":1568014460893,               // Event Time
    "o":{
        "s":"BTCUSDT",             // Symbol
        "S":"SELL",                // Side
        "o":"LIMIT",               // Order Type
        "f":"IOC",                 // Time in Force
        "q":"0.014",               // Original Quantity
        "p":"9910",                // Price
        "ap":"9910",               // Average Price
        "X":"FILLED",              // Order Status
        "l":"0.014",               // Order Last Filled Quantity
        "z":"0.014",               // Order Filled Accumulated Quantity
        "T":1568014460893            // Order Trade Time
    }
}
```



## Target Coins untuk Monitoring
- XRP (XRPUSDT)
- DOGE (DOGEUSDT) 
- PEPE (PEPEUSDT)

## WebSocket Streams yang Diperlukan
- xrpusdt@forceOrder
- dogeusdt@forceOrder
- pepeusdt@forceOrder

