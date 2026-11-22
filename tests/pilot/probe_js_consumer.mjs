#!/usr/bin/env node
// Offline behavioral probe for the JS SDK vendored by Arvectum Site.
// Run with an explicit local extracted SDK path; mock every fetch call.
import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
const path = process.argv[2];
if (!path || !path.endsWith(".mjs")) throw new Error("Provide extracted Site SDK .mjs path");
const { DataPlatformClient, DataPlatformError } = await import(pathToFileURL(path).href);
const cases = ["health","contract_v1","contract_v2_rejected",
 "exists_200","exists_404","stats_503","stats_401",
 "search_identity","ensure_404_create","transport_failure"];
const scenarios = {};
for (const testCase of cases) {
  const seen = [];
  const fetchImpl = async (url, options = {}) => {
    const method = options.method || "GET";
    const pathname = decodeURIComponent(new URL(url).pathname);
    seen.push([method, pathname]);
    if (testCase === "transport_failure") throw new Error("synthetic offline network failure");
    if (testCase === "search_identity") {
      assert.equal(method, "POST");
      assert.equal(pathname, "/v1/search");
      assert.equal(options.headers["X-Arvectum-Consumer"],"fixture-consumer");
      assert.equal(options.headers["X-Arvectum-Consumer-Key"],"fixture-not-a-secret");
      const payload = JSON.parse(options.body);
      assert.equal(payload.query,"кабель");
      assert.deepEqual(payload.collections,["fixture:docs"]);
      assert.equal(payload.vector_weight,4);
      return Response.json({ query:"кабель",hits:[] },{status:200});
    }
    if (testCase === "health") {
      assert.equal(pathname,"/health");
      return Response.json({status:"ok"});
    }
    if (testCase.startsWith("contract_v")) {
      assert.equal(pathname,"/v1/contract");
      return Response.json({version:testCase==="contract_v2_rejected"?"2.0":"1.0"});
    }
    if (testCase.startsWith("exists")) {
      assert.equal(pathname,"/v1/collections/fixture:docs");
      return Response.json({}, {status:testCase==="exists_200"?200:404});
    }
    if (testCase.startsWith("stats")) {
      assert.equal(pathname,"/v1/collections/fixture:docs/stats");
      return Response.json({detail:"fixture"}, {status:Number(testCase.slice(-3))});
    }
    if (testCase === "ensure_404_create") {
      if (method==="GET") {
        assert.equal(pathname,"/v1/collections/fixture:docs");
        return Response.json({}, {status:404});
      }
      assert.equal(method,"POST");
      assert.equal(pathname,"/v1/collections");
      const payload=JSON.parse(options.body);
      assert.equal(payload.collection_id,"fixture:docs");
      assert.equal(payload.owner,"fixture-owner");
      return Response.json({collection_id:"fixture:docs",owner:"fixture-owner"});
    }
    throw new Error("Unknown case "+testCase);
  };
  const client = new DataPlatformClient({
    baseUrl:"http://sdk-fixture.invalid",
    apiKey:"fixture-internal",
    consumer:"fixture-consumer",
    consumerKey:"fixture-not-a-secret",
    fetchImpl
  });
  let outcome;
  try {
    if (testCase === "health") {
      assert.equal((await client.health()).status,"ok");
      outcome="ok";
    } else if (testCase==="contract_v1") {
      assert.equal((await client.requireContract(1)).version,"1.0");
      outcome="ok";
    } else if (testCase==="contract_v2_rejected") {
      await client.requireContract(1);
      throw new Error("incompatible major accepted");
    } else if (testCase.startsWith("exists")) {
      const exists=await client.collectionExists("fixture:docs");
      assert.equal(exists,testCase==="exists_200");
      outcome=exists?"present":"absent";
    } else if (testCase.startsWith("stats")) {
      await client.collectionStats("fixture:docs");
      throw new Error("HTTP failure accepted");
    } else if (testCase==="search_identity") {
      const result=await client.search({query:"кабель",collections:["fixture:docs"],limit:5,vectorWeight:4});
      assert.deepEqual(result.hits,[]);
      outcome="hits_empty";
    } else if (testCase==="ensure_404_create") {
      const result=await client.ensureCollection("fixture:docs",{name:"Fixture",owner:"fixture-owner"});
      assert.equal(result.collection_id,"fixture:docs");
      outcome="created";
    } else if (testCase==="transport_failure") {
      await client.health();
      throw new Error("transport failure accepted");
    }
  } catch (error) {
    if (!(error instanceof DataPlatformError)) throw error;
    if (testCase==="stats_503" || testCase==="stats_401") {
      assert.equal(error.status,Number(testCase.slice(-3)));
      assert.equal(error.method,"GET");
      outcome="http_"+error.status;
    } else if (testCase==="contract_v2_rejected") {
      outcome="incompatible_contract";
    } else if (testCase==="transport_failure") {
      outcome="transport_error";
    } else {
      throw error;
    }
  }
  assert.ok(outcome,"missing probe outcome");
  if (testCase==="ensure_404_create") {
    assert.deepEqual(seen,[["GET","/v1/collections/fixture:docs"],["POST","/v1/collections"]]);
  } else {
    assert.equal(seen.length,1);
  }
  scenarios[testCase]=outcome;
}
console.log(JSON.stringify({schema:"aec001-two-consumer-contract-v1",language:"JavaScript",scenarios}));
