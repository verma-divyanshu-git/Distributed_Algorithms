package RMI;

import java.rmi.Naming;

// Client code
public class RMIClient {
    public static void main(String[] args) {
        try {
            // Lookup the remote object
            Hello obj = (Hello) Naming.lookup("rmi://localhost:1099/HelloService");
            
            // Call the remote method and print the response
            String message = obj.sayHello();
            System.out.println("Message from Server: " + message);
        } catch (Exception e) {
            System.out.println("Client exception: " + e.toString());
            e.printSta  ckTrace();
        }
    }
}
