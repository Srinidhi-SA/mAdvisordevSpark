var path = require("path");
var _datepicker =  'react-dates/lib/css/_datepicker.css';

var DIST_DIR = path.resolve(__dirname, "dist");
var SRC_DIR = path.resolve(__dirname, "src");
var ASSETS_DIR = path.resolve(__dirname,"assets");
//const webpack = require('webpack')
//var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const env = process.env.npm_lifecycle_event;
var config = {
    entry: SRC_DIR + "/app/index.js",
    output: {
        path: DIST_DIR + "/app",
        filename: "bundle.js",
        publicPath: "/app/"
    },
    devtool: env === "buildDev" ? "eval" : "eval-source-map",
    module: {
        loaders: [
          {
            test: /\.jsx?$/,
            exclude: /(node_modules|bower_components)/,
            loader: 'babel-loader',
            query: {
              presets: ['react', 'es2015', 'stage-0'],
              plugins: ['react-html-attrs', 'transform-class-properties', 'transform-decorators-legacy'],
            }
          }
        ]
    },
    devServer: {
      historyApiFallback: true
    },
};

module.exports = config;
