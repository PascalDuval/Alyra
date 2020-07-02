const fetch = require('node-fetch') // Fetch library pour Node
const url = 'https://api-pub.bitfinex.com/v2/'// Domaine

const pathParams = 'trades/tBTCUSD/hist' // tBTCUSD, tETHUSD, tBTCUST .. cf docs API https://docs.bitfinex.com/reference#rest-public-tickers
const queryParams = 'limit=1&sort=-1' // l'API permet de sortir plusieurs 


console.log("On fetch ici le dernier trade BTC -> USD sur Bitfinex")

async function request() {
    try {
        const req = await fetch(`${url}/${pathParams}?${queryParams}`)
        const response = await req.json()
        console.log(`${JSON.stringify(response)}`) // Le prix de cet dernier échange BTC -> USD est dans le dernier élément du tableau
        console.log("1 . Le premier élément est l'ID du trade")
        console.log("2 . Le deuxième élement est le time stamp en millisecond de ce trade")
	console.log("3 . Le deuxième est ±AMOUNT : positif si achat, négatif si vente")
        console.log("4 . Le prix de ce dernier échange BTC -> USD est dans le dernier élément de cette liste") // Le prix de cet dernier échange BTC -> USD est dans le dernier élément du tableau
    }
    catch (err) { 
        console.log(err) // Catch et logs en cas d'erreur
    }
}

request()





