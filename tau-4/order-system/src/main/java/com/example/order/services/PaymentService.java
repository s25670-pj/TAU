package com.example.order.services;

public interface PaymentService {
    boolean processPayment(String userId, String productId);
}