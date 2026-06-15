import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // cacheComponents: true,
  output: 'standalone',
  allowedDevOrigins: ['digicod.eu','.digicod.eu', 'shop.digicod.eu', '*','localhost:3000'],
  async rewrites() {
    return [
      {
        source: '/:path*', // Anfragen an /api werden weitergeleitet
        destination: 'https://shop.digicod.eu/:path*', // Backend-URL
      },
    ];
  },
};

export default nextConfig;
