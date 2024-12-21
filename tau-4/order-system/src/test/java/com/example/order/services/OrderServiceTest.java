package com.example.order.services;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class OrderServiceTest {
    private OrderService orderService;
    private PaymentService paymentServiceMock;
    private InventoryService inventoryServiceMock;
    private NotificationService notificationServiceMock;

    private final String productId = "1";
    private final String userId = "1";

    @BeforeEach
    void setUp() {
        paymentServiceMock = mock(PaymentService.class);
        inventoryServiceMock = mock(InventoryService.class);
        notificationServiceMock = mock(NotificationService.class);

        orderService = new OrderService(paymentServiceMock, inventoryServiceMock, notificationServiceMock);
    }

    @Test
    @DisplayName("Verify successful purchase flow with all conditions met")
    void verifySuccessfulPurchaseFlow() {
        when(inventoryServiceMock.isProductAvailable(productId)).thenReturn(true);
        when(paymentServiceMock.processPayment(userId, productId)).thenReturn(true);

        boolean result = orderService.placeOrder(userId, productId);

        assertTrue(result);
        verify(inventoryServiceMock).isProductAvailable(productId);
        verify(paymentServiceMock).processPayment(userId, productId);
        verify(notificationServiceMock).sendNotification(eq(userId), eq("Your order has been confirmed and is being processed"));
    }

    @Test
    @DisplayName("Validate inventory check prevents order when stock unavailable")
    void validateInventoryCheckPreventsOrder() {
        when(inventoryServiceMock.isProductAvailable(productId)).thenReturn(false);

        boolean result = orderService.placeOrder(userId, productId);

        assertFalse(result);
        verify(inventoryServiceMock).isProductAvailable(productId);
        verifyNoInteractions(paymentServiceMock);
        verify(notificationServiceMock).sendNotification(eq(userId), eq("Sorry, this item is currently out of stock"));
    }

    @Test
    @DisplayName("Confirm order rejection when payment transaction fails")
    void confirmOrderRejectionOnPaymentFailure() {
        when(inventoryServiceMock.isProductAvailable(productId)).thenReturn(true);
        when(paymentServiceMock.processPayment(userId, productId)).thenReturn(false);

        boolean result = orderService.placeOrder(userId, productId);

        assertFalse(result);
        verify(inventoryServiceMock).isProductAvailable(productId);
        verify(paymentServiceMock).processPayment(userId, productId);
        verify(notificationServiceMock).sendNotification(eq(userId), eq("Transaction declined: Unable to process payment"));
    }

    @Test
    @DisplayName("Ensure system resilience when payment service encounters error")
    void ensureSystemResilienceOnPaymentError() {
        when(inventoryServiceMock.isProductAvailable(productId)).thenReturn(true);
        when(paymentServiceMock.processPayment(userId, productId)).thenThrow(new RuntimeException("Payment service error"));

        boolean result = orderService.placeOrder(userId, productId);

        assertFalse(result);
        verify(inventoryServiceMock).isProductAvailable(productId);
        verify(paymentServiceMock).processPayment(userId, productId);
        verify(notificationServiceMock).sendNotification(eq(userId), eq("Technical difficulties encountered. Please try again later"));
    }
}