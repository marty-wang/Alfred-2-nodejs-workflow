#!/usr/bin/env node

process.argv.forEach(function(val, index, array) {
  if (index > 1) {
      console.log(index + ': ' + val);
  }
});