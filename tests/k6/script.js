import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Counter, Trend } from 'k6/metrics';

export let httpStatus = new Counter('http_status');
export let httpLatency = new Trend('http_latency', true);

export let options = {
  stages: [
    { duration: '1m', target: 20 },  // sobe até 20 VUs em 1m
    { duration: '2m', target: 50 },  // mantém 50 VUs por 2m
    { duration: '1m', target: 0 },   // desliga em 1m
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
  ext: {
    influxdb: {
      address: 'http://localhost:8086',
      database: 'k6',
      tags: { project: 'restaurant', env: 'dev' },
    },
  },
};

const BASE = 'http://localhost:5000/restaurant';

export default function () {
  // ---- GET /dishes ----
  group('GET /dishes', () => {
    let res = http.get(`${BASE}/dishes`);
    httpStatus.add(1, { status: res.status, method: 'GET' });
    httpLatency.add(res.timings.duration, { method: 'GET' });
    check(res, { 'status 200': (r) => r.status === 200 });
  });

  // ---- POST → PUT → DELETE /dishes ----
  group('POST→PUT→DELETE /dishes', () => {
    // POST
    let payload = JSON.stringify({
      name: `Prato K6 ${Math.random().toString(36).slice(2)}`,
      description: 'Teste de carga',
      price: (Math.random() * 100).toFixed(2),
    });
    let res = http.post(`${BASE}/dishes`, payload, {
      headers: { 'Content-Type': 'application/json' },
    });
    httpStatus.add(1, { status: res.status, method: 'POST' });
    httpLatency.add(res.timings.duration, { method: 'POST' });
    check(res, { 'created 201': (r) => r.status === 201 });
    let id = res.json('id');
    sleep(0.5);

    // PUT
    let resPut = http.put(
      `${BASE}/dishes/${id}`,
      JSON.stringify({ name: 'Atualizado K6' }),
      { headers: { 'Content-Type': 'application/json' } }
    );
    httpStatus.add(1, { status: resPut.status, method: 'PUT' });
    httpLatency.add(resPut.timings.duration, { method: 'PUT' });
    check(resPut, { 'updated 200': (r) => r.status === 200 });
    sleep(0.5);

    // DELETE
    let resDel = http.del(`${BASE}/dishes/${id}`);
    httpStatus.add(1, { status: resDel.status, method: 'DELETE' });
    httpLatency.add(resDel.timings.duration, { method: 'DELETE' });
    check(resDel, { 'deleted 204': (r) => r.status === 204 });
    sleep(1);
  });
}
