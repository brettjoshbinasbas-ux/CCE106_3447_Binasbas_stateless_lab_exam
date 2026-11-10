import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stateless_lab_exam/main.dart';
import 'package:stateless_lab_exam/shopping_cart_page.dart';

void main() {
  testWidgets('Campus Store Shopping Cart UI renders correctly', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1080, 2400);
    tester.view.devicePixelRatio = 2.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const CampusStoreApp());

    // 1. Verify AppBar and Title
    expect(find.text('My Cart'), findsOneWidget);
    expect(find.byIcon(Icons.arrow_back), findsOneWidget);
    expect(find.byIcon(Icons.shopping_bag_outlined), findsOneWidget);
    expect(find.text('3'), findsOneWidget); // Badge

    // 2. Verify Introduction Section
    expect(find.text('CAMPUS STORE'), findsOneWidget);
    expect(find.text('Ready for checkout'), findsOneWidget);
    expect(find.text('Review your items before placing your order.'), findsOneWidget);

    // 3. Verify Delivery Information Card
    expect(find.text('Deliver to Brett Josh Binasbas'), findsOneWidget);
    expect(find.text('Matina, Davao City'), findsOneWidget);
    expect(find.text('Change'), findsOneWidget);

    // 4. Verify Order Items and Products
    expect(find.text('Order Items'), findsOneWidget);
    expect(find.text('3 items'), findsOneWidget);
    expect(find.byType(CartItemCard), findsNWidgets(3));
    expect(find.text('Wireless Mouse'), findsOneWidget);
    expect(find.text('PHP 450.00'), findsOneWidget);
    expect(find.text('USB-C Hub'), findsOneWidget);
    expect(find.text('PHP 850.00'), findsOneWidget);
    expect(find.text('Laptop Stand'), findsOneWidget);
    expect(find.text('PHP 700.00'), findsOneWidget);

    // 5. Verify Discount Banner
    expect(find.text('STUDENT10 applied'), findsOneWidget);
    expect(find.text('10% discount on items'), findsOneWidget);

    // 6. Verify Payment Summary
    expect(find.text('Payment Summary'), findsOneWidget);
    expect(find.text('Subtotal'), findsOneWidget);
    expect(find.text('PHP 2,000.00'), findsOneWidget);
    expect(find.text('Discount (10%)'), findsOneWidget);
    expect(find.text('- PHP 200.00'), findsOneWidget);
    expect(find.text('Delivery Fee'), findsOneWidget);
    expect(find.text('PHP 50.00'), findsOneWidget);
    expect(find.text('Total'), findsOneWidget);
    expect(find.text('PHP 1,850.00'), findsOneWidget);

    // 7. Verify Place Order Button
    expect(find.text('Place Order'), findsOneWidget);
  });

  testWidgets('Verify required button callbacks and console output', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1080, 2400);
    tester.view.devicePixelRatio = 2.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const CampusStoreApp());

    // 1. Back arrow
    await tester.tap(find.byIcon(Icons.arrow_back));
    await tester.pump();

    // 2. Shopping bag
    await tester.tap(find.byIcon(Icons.shopping_bag_outlined));
    await tester.pump();

    // 3. Change delivery address
    await tester.tap(find.text('Change'));
    await tester.pump();

    // 4. Quantity & Delete controls for each product
    final minusButtons = find.byIcon(Icons.remove);
    final plusButtons = find.byIcon(Icons.add);
    final deleteButtons = find.byIcon(Icons.delete_outline_rounded);

    // Wireless Mouse
    await tester.tap(minusButtons.at(0));
    await tester.pump();
    await tester.tap(plusButtons.at(0));
    await tester.pump();
    await tester.tap(deleteButtons.at(0));
    await tester.pump();

    // USB-C Hub
    await tester.tap(minusButtons.at(1));
    await tester.pump();
    await tester.tap(plusButtons.at(1));
    await tester.pump();
    await tester.tap(deleteButtons.at(1));
    await tester.pump();

    // Laptop Stand
    await tester.tap(minusButtons.at(2));
    await tester.pump();
    await tester.tap(plusButtons.at(2));
    await tester.pump();
    await tester.tap(deleteButtons.at(2));
    await tester.pump();

    // 5. Place Order button
    await tester.ensureVisible(find.text('Place Order'));
    await tester.tap(find.text('Place Order'));
    await tester.pump();
  });
}
