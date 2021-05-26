pragma solidity ^0.5.0;

// Importing the Mintable Token from the local directory.
import "./PupperCoin.sol";

// Don't Reinvent the wheel. Use premade libraries.
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";

// Which libraries will this contract use
contract PupperCoinSale is Crowdsale, MintedCrowdsale, TimedCrowdsale{

    constructor(
        // Defining some characteristics of the contract.
        PupperCoin token,
        string symbol,
        address payable wallet,
        uint goal,
        uint rate,
        // These are found in the TimeCrowdsale Contract from the import above
        uint openingTime
        uint closingTime
    )
        // Pass the constructor parameters to the crowdsale contracts.
        RefundableCrowdsale(goal)
        Crowdsale(rate, wallet, token)
        // For this one, you have to look into the actual TimedCrowdsale Contract to know what paramaters it takes.
        TimedCrowdsale(openingTime, closingTime)
        public

    {
        // constructor can stay empty
    }
}

contract PupperCoinSaleDeployer {
    // Deploying a contract within a contract: https://docs.openzeppelin.com/contracts/2.x/crowdsales
    address public token_sale_address;
    address public token_address;

    constructor(
        // @TODO: Fill in the constructor parameters!
    )
        public
    {
        // @TODO: create the PupperCoin and keep its address handy

        // @TODO: create the PupperCoinSale and tell it about the token, set the goal, and set the open and close times to now and now + 24 weeks.

        // make the PupperCoinSale contract a minter, then have the PupperCoinSaleDeployer renounce its minter role
        token.addMinter(token_sale_address);
        token.renounceMinter();
    }
}
