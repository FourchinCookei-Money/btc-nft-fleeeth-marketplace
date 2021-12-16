require("@nomiclabs/hardhat-waffle");
const fs = require('fs');
// const privateKey = fs.readFileSync(".secret").toString().trim() || "f8aae46a0c69407aacef4c2a1e748596";
// const infuraId = fs.readFileSync(".infuraid").toString().trim() || "23729665ba9543a981510918a6a4b835";
module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      chainId: 1337
    },
    /*
    mumbai: {
      // Infura
      // url: `https://polygon-mumbai.infura.io/v3/${infuraId}`
      url: "https://rpc-mumbai.matic.today",
      accounts: [privateKey]
    },
     metis (Arbitrum-Rinkeby): {
      // Infura
      // url: `https://arbitrum-rinkeby.infura.io/v3/${infuraId}`
      url: "https://rinkeby.arbitrum.io/rpc",
      accounts: [privateKey]
     },
     matic: {
      // Infura
      // url: `https://polygon-mainnet.infura.io/v3/${infuraId}`,
      url: "https://rpc-mainnet.maticvigil.com",
      accounts: [privateKey]
      },
       */
         },
    solidity: {
      version: "0.8.4",
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
      }
    }
  }

};
