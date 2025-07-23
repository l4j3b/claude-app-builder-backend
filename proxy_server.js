const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();

// Proxy Claude API
app.use(
  "/code-api",
  createProxyMiddleware({
    target: "http://localhost:8000",
    changeOrigin: true,
  })
);

// Proxy Next.js app
app.use(
  "/",
  createProxyMiddleware({
    target: "http://localhost:3001",
    changeOrigin: true,
  })
);

app.listen(3000, "0.0.0.0", () => console.log("Proxy listening on port 3000"));
