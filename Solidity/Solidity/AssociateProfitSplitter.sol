pragma solidity ^0.5.0;

// lvl 1: equal split
contract AssociateProfitSplitter {
    // Defining who the employees are.
        address payable employee_one;
        address payable employee_two;
        address payable employee_three;

    // Telling Solidity that these are the only three accounts to be considered in this contract.
    constructor(
        address payable _one, 
        address payable _two, 
        address payable _three
        
        ) public {
            
        employee_one = _one;
        employee_two = _two;
        employee_three = _three;
    }
    // Getting the balance of this contract
    function balance() public view returns(uint) {
        return address(this).balance;
    }
    function deposit() public payable {
        // The amount is specified by the account who runs this transaction.
        // This is also the account that get's charged the gas fee.
        uint amount = msg.value / 3;


        // Transfer the amount to each employee
        employee_one.transfer(amount);
        employee_two.transfer(amount);
        employee_three.transfer(amount);

        //take care of a potential remainder by sending back to HR (`msg.sender`)
        msg.sender.transfer(msg.value - amount * 3);
    }
    // Calling the deposit in the fallback function to help reduce errors.
    // If this function cannot be completed, then no gas will be spent.
    function() external payable {
        deposit();
    }
}
