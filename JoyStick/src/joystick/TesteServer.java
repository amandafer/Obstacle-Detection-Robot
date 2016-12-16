/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package joystick;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class TesteServer
{
    private final static int PACKETSIZE = 100;
    
    public static void main(String[] args) 
    {        
        try 
        {
            // Convert the argument to ensure that is it valid
            int port = Integer.parseInt("5005");

            // Construct the socket
            DatagramSocket socket = new DatagramSocket(port);

            System.out.println("The server is ready...");

            for(;;)
            {
                // Create a packet
                DatagramPacket packet = new DatagramPacket(new byte[PACKETSIZE], PACKETSIZE);

                // Receive a packet (blocking)
                socket.receive(packet);

                // Print the packet
                System.out.println(packet.getAddress() + " " + packet.getPort() + ": " + new String(packet.getData()));

                // Return the packet to the sender
                socket.send(packet);
            }
        }
        catch(Exception ex) 
        {
            Logger.getLogger(TesteServer.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}
