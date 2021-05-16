
// This class is for Q9
public class BankAccount {
    private double balance;

    public BankAccount() {
        balance = 500;
    }

    public BankAccount(double b) {
        balance = b;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        balance += amount;
    }

    public boolean withdraw(double amount) {
        if (amount > balance)
            return false;
        
        balance -= amount;
        return true;
    }

    public boolean transfer(double amount, BankAccount otherAccount) {
        if (amount > balance)
            return false;
        
        balance -= amount;
        otherAccount.deposit(amount);
        return true;
    }
}