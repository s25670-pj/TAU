package com.example.order.services;

public class OrderService {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    public OrderService(PaymentService paymentService, InventoryService inventoryService, NotificationService notificationService) {
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
        this.notificationService = notificationService;
    }

    public boolean placeOrder(String userId, String productId) {
        if (!inventoryService.isProductAvailable(productId)) {
            notificationService.sendNotification(userId, "Sorry, this item is currently out of stock");
            return false;
        }

        try {
            if (paymentService.processPayment(userId, productId)) {
                notificationService.sendNotification(userId, "Your order has been confirmed and is being processed");
                return true;
            } else {
                notificationService.sendNotification(userId, "Transaction declined: Unable to process payment");
                return false;
            }
        } catch (Exception e) {
            notificationService.sendNotification(userId, "Technical difficulties encountered. Please try again later");
            return false;
        }
    }
}