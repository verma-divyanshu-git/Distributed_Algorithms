package RMI;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

// Server code
public class RMIServer {
    public static void main(String[] args) {
        try {
            // Start RMI registry programmatically
            LocateRegistry.createRegistry(1099);
            
            // Create an instance of HelloImpl
            HelloImpl obj = new HelloImpl();
            
            // Bind the remote object to the registry
            Naming.rebind("HelloService", obj);
            
            System.out.println("Server is ready.");
        } catch (Exception e) {
            System.out.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
