/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Pointing to the ui directory for App Router
  // Next.js expects app/ inside the root or src/ or specified via some config.
  // Since we have ui/app, we need to make sure Next.js picks it up.
  // In Next.js 14, it defaults to looking in root/app or root/src/app.
  // We might need to move ui/app to app/ or use a custom pages/app directory config if supported,
  // but usually it's easier to follow the convention or use a symlink if we must keep the 'ui' prefix.
  // However, some versions of Next allow custom root.
};

module.exports = nextConfig;
