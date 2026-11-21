#!/usr/bin/env python3
"""Pure mock HTTP contract probe of the installed Tender Agent Data Platform SDK.

Run with Tender's trusted installed Python runtime; never contacts a service.
A private fixture credential is synthetic and not read from the environment.
"""
import json
import sys

import httpx
from arvectum_data_client import DataPlatformClient, DataPlatformError

EXPECTED = ("health", "contract_v1", "contract_v2_rejected",
            "exists_200", "exists_404", "stats_503", "stats_401",
            "search_identity", "ensure_404_create", "transport_failure")
RESULTS = {}

def assert_equal(actual, expected, what):
    if actual != expected:
        raise AssertionError(f"{what}: expected {expected!r}, got {actual!r}")

for case in EXPECTED:
    seen = []
    def handler(request):
        path = request.url.path
        seen.append((request.method, path))
        if case == "transport_failure":
            raise httpx.ConnectError("synthetic offline network failure", request=request)
        if case == "search_identity":
            assert_equal(request.method, "POST", "search verb")
            assert_equal(path, "/v1/search", "search path")
            assert_equal(request.headers.get("X-Arvectum-Consumer"), "fixture-consumer", "search principal")
            assert_equal(request.headers.get("X-Arvectum-Consumer-Key"), "fixture-not-a-secret", "search fixture token")
            data = json.loads(request.content)
            assert_equal(data["query"], "кабель", "query")
            assert_equal(data["collections"], ["fixture:docs"], "collections")
            assert_equal(data["vector_weight"], 4.0, "vector weight")
            return httpx.Response(200, json={"query":"кабель","hits":[]})
        if case == "health":
            assert_equal(path, "/health", "health path")
            return httpx.Response(200,json={"status":"ok"})
        if case.startswith("contract_v"):
            assert_equal(path,"/v1/contract","contract path")
            version = "2.0" if case == "contract_v2_rejected" else "1.0"
            return httpx.Response(200,json={"version":version})
        if case.startswith("exists"):
            assert_equal(path,"/v1/collections/fixture:docs","collection exists path")
            return httpx.Response(200 if case.endswith("200") else 404,json={})
        if case.startswith("stats"):
            assert_equal(path,"/v1/collections/fixture:docs/stats","collection stats path")
            return httpx.Response(int(case[-3:]),json={"detail":"fixture"})
        if case == "ensure_404_create":
            if request.method=="GET":
                assert_equal(path,"/v1/collections/fixture:docs","create lookup")
                return httpx.Response(404,json={})
            assert_equal(request.method,"POST","create verb")
            assert_equal(path,"/v1/collections","create path")
            payload=json.loads(request.content)
            assert_equal(payload["collection_id"],"fixture:docs","created collection")
            assert_equal(payload["owner"],"fixture-owner","created owner")
            return httpx.Response(200,json={"collection_id":"fixture:docs","owner":"fixture-owner"})
        raise AssertionError(f"unknown case {case}")
    http = httpx.Client(base_url="http://sdk-fixture.invalid", transport=httpx.MockTransport(handler),
                        headers={"X-Arvectum-Key":"fixture-internal"})
    client = DataPlatformClient(base_url="http://sdk-fixture.invalid",client=http,
                                consumer="fixture-consumer",consumer_key="fixture-not-a-secret")
    try:
        try:
            if case=="health":
                assert_equal(client.health()["status"],"ok","health result")
                result = "ok"
            elif case=="contract_v1":
                assert_equal(client.require_contract(1)["version"],"1.0","contract version")
                result = "ok"
            elif case=="contract_v2_rejected":
                client.require_contract(1)
                raise AssertionError("incompatible major was accepted")
            elif case.startswith("exists"):
                exists=client.collection_exists("fixture:docs")
                assert_equal(exists,case=="exists_200","existence")
                result = "present" if exists else "absent"
            elif case.startswith("stats"):
                client.collection_stats("fixture:docs")
                raise AssertionError("HTTP error was accepted")
            elif case=="search_identity":
                hits=client.search(query="кабель",collections=["fixture:docs"],limit=5,
                                   vector_weight=4.0)
                assert_equal(hits,[],"search hits")
                result="hits_empty"
            elif case=="ensure_404_create":
                created=client.ensure_collection(collection_id="fixture:docs",name="Fixture",
                                                 owner="fixture-owner")
                assert_equal(created["collection_id"],"fixture:docs","collection id")
                result="created"
            elif case=="transport_failure":
                client.health()
                raise AssertionError("transport error was accepted")
        except DataPlatformError as error:
            if case in ("stats_503","stats_401"):
                assert_equal(error.status_code,int(case[-3:]),"status")
                assert_equal(error.method,"GET","failed method")
                result=f"http_{error.status_code}"
            elif case=="contract_v2_rejected":
                result="incompatible_contract"
            elif case=="transport_failure":
                result="transport_error"
            else:
                raise
        expected_verb={"search_identity":"POST"}
        if case=="ensure_404_create":
            assert_equal(seen,[("GET","/v1/collections/fixture:docs"),
                               ("POST","/v1/collections")],"creation sequence")
        elif case=="transport_failure":
            assert_equal(len(seen),1,"failed request count")
        else:
            assert_equal(len(seen),1,"request count")
        RESULTS[case]=result
    finally:
        http.close()

print(json.dumps({"schema":"aec001-two-consumer-contract-v1",
                  "language":"Python","scenarios":RESULTS},sort_keys=True))
