import axios from 'axios';
import express from 'express';
import Router from 'express-promise-router';
import { createClient } from 'redis';


const app = express();
const router = Router();
const port = process.env.PORT || 8080;
const redisPassword = process.env.JETPACK_RUNTIME_REDIS_PASSWORD;
const redisUrl = `redis://:${redisPassword}@jetpack-runtime-redis-master:6379`;


const redisClient = createClient({
  url: redisUrl
});
redisClient.connect(); // but don't await, ASSUME: it started before requests arrive

redisClient.on('error', (err) => {
  console.log(err)
});

redisClient.on('connect', () => {
  console.log('Redis connected!')
});


router.get('/', (req, res) => {
  return res.json({
    '/repos?search={name}': 'Get the GitHub profile details for this user',
    '/cache': 'Get all cached data in Redis',
    '/autoscale': 'Make Kubernetes scale horizontally by consuming all the CPU',
    '/env': 'Get the environment variables'
  });
});

// show all the environment variables
router.get('/env', (req, res) => {
  return res.json(process.env); // Great for understanding Jetpack, FRAGILE: security hole
});

// make Kubernetes scale horizontally by consuming all the CPU
// kubectl get all to see multiple pods
router.get('/autoscale', function(_, res) {
  let total = 0;
  for (let i = 0; i < 1000000000; i++) {
    total += Math.sqrt(i + 0.123);
  }
  return res.json({ total });
});

// get the contents of the Redis cache
router.get('/cache', async (req, res) => {
  const keys = await redisClient.keys('*');
  const values = await Promise.all(keys.map(async (key) => {
    try {
      return await redisClient.get(key)
    } catch (err) {
      return { err: { message: err.message } };
    }
  }));
  const results = {};
  for (let i = 0; i < keys.length; i++) {
    results[keys[i]] = values[i]; // TODO: JSON.parse? value may not be JSON.
  }
  return res.json(results);
});

router.get('/repos', async (req, res) => {
  const searchTerm = req.query.search;
  if (!searchTerm) {
    return res.status(400).json({message: 'set search in query string'});
  }
  const results = await redisClient.get(searchTerm);
  if (results) {
    // return cached results
    return res.status(200).send({
      message: 'cache hit',
      results: JSON.parse(results)
    });
  } else {
    // get new results and cache
    const results = await axios.get(`https://api.github.com/search/repositories?q=${searchTerm}`);
    const parsed = parseSearchResults(results.data, searchTerm)
    await redisClient.set(searchTerm, JSON.stringify(parsed), 'EX', 600); // expire in 60 seconds
    return res.status(200).send({
      message: 'cache miss',
      results: parsed
    });
  }
});

const parseSearchResults = function(res, query) {
  if (!res) {
    return { query };
  }
  let totalCount = res.total_count;
  let topRepos = res.items.slice(0, 10).map(x => ({ name: x.full_name, url: x.html_url }));
  return { totalCount, topRepos, query };
}


app.use('/', router);

app.use((err, req, res, next) => {
  console.log(`Request error: ${err.message}`);
  console.error({err, stack: err.stack});
  res.status(500).send('Something broke!');
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
