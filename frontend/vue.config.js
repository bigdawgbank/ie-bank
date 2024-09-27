const { defineConfig } = require("@vue/cli-service");
const dotenv = require("dotenv");
const path = require("path");

// Load .env file from the root of the project
dotenv.config({ path: path.resolve(__dirname, "../.env") });

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    devtool: "source-map",
  },
});

