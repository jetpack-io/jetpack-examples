'use strict';

import express from 'express';
import { createClient } from '@node-redis/client';
import axios from 'axios';

const app = express()
const port = 8080
const redisPassword = process.env.JETPACK_RUNTIME_REDIS_PASSWORD
const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

const redisClient = createClient({
    url: `redis://:${redisPassword}@jetpack-runtime-redis-master:6379`
});

const parseSearchResults = function(res, searchTerm) {
    // console.log(res)
    let totalCount = res.total_count
    let topRepos = res.items.slice(0, 10).map(x => {
        return { name: x.full_name, url: x.html_url }
    })
    return { totalCount: totalCount, topRepos: topRepos, query: searchTerm }
}

app.set('views', './views')
app.set('view engine', 'pug')

app.get('/', (_, res) => {
    res.send('Hello World!')
})

app.get('/stall', function(_, res) {
    var total = 0
    for (let i = 0; i < 1000000000; i++) {
        total += Math.sqrt(i + 0.123)
    }
    res.send(`Total: ${total}`)
})

app.get('/repos', async function(req, res) {
    const searchTerm = req.query.search;
    console.log("Checking Cache...");
    await redisClient.connect()
    try {
        let results = await redisClient.get(searchTerm)
        if (results) {
            console.log("Cache Success")
            let repoData = parseSearchResults(JSON.parse(results), searchTerm)
            res.status(200).render('repos', repoData);
        } else {
            console.log("Cache Miss")
            const searchResults =
                await (async() => {
                    let results = await axios.get(`https://api.github.com/search/repositories?q=${searchTerm}&sort=stars`);
                    await redisClient.set(searchTerm, JSON.stringify(results.data), {
                        EX: 600
                    });
                    await redisClient.disconnect()
                    return results
                })()
            let repoData = parseSearchResults(searchResults.data, searchTerm)
            res.status(200).render('repos', repoData);
        }
    } catch (err) {
        console.log(err)
        res.status(500).send({ message: err.message });
    } finally {
        if (redisClient.isOpen) {
            await redisClient.quit()
        }
    }
})



redisClient.on("error", (err) => {
    console.log(err)
})

redisClient.on("connect", () => {
    console.log("Connected!")
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})