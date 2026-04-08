import json

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }

cells = []

# 1. Introduction
cells.append(create_markdown_cell("""# Customer Support Prompt Library & Evaluation Report

## 1. Introduction
Welcome to the **Customer Support Prompt Library and Evaluation Report**. This notebook is designed for customer support teams to build, manage, and evaluate reusable AI prompts. 

The goal is to generate outputs that simulate real-world support responses and adhere to best practices for:
- **Tone:** Professional, empathetic, and helpful.
- **Efficiency:** Quick resolution with minimal back-and-forth.
- **Accuracy:** Correct information aligned with company policies.

### Evaluation Framework
Each prompt's output will be evaluated on a **1–5 scale** based on the following criteria:
1. **Clarity:** Is the response easy to understand and well-structured?
2. **Accuracy:** Does it provide correct and relevant information based on the prompt's constraints?
3. **Conciseness:** Is it free from unnecessary verbosity while still being polite?

Let's explore the prompts across three key areas: Order Status Inquiries, Troubleshooting Guides, and Refund Requests.
"""))

# 2. Prompt Templates + Outputs
cells.append(create_markdown_cell("""## 2. Prompt Templates + Outputs

### Category A: Order Status Inquiries
"""))

cells.append(create_markdown_cell("""#### Prompt 1: Standard Shipping Update
**Prompt:**
> "Act as a helpful customer support agent for 'TechGadget'. A customer named Alice asks where her order #12345 is. It shipped yesterday and will arrive in 2 days. Write a concise, reassuring message."

**Sample Output:**
> "Hi Alice! Thank you for reaching out to TechGadget. I'm happy to let you know that your order #12345 successfully shipped yesterday. It is currently on its way and is expected to arrive within 2 days. We will send you another update once it is out for delivery. Please let us know if you have any other questions!"
"""))

cells.append(create_markdown_cell("""#### Prompt 2: Delayed Order Apology
**Prompt:**
> "Customer Bob ordered a laptop 5 days ago, but it is delayed by a week due to unforeseen stock issues. Draft an empathetic apology email offering a 10% discount code (DELAY10) on his next purchase for the inconvenience."

**Sample Output:**
> "Dear Bob, I’m writing to sincerely apologize regarding your recent laptop order. Unfortunately, due to unexpected delays in our supply chain, your shipment will be delayed by approximately one week. We know how frustrating it is to wait for a new device, and we are working hard to expedite things on our end. As a token of our apology, please accept this 10% discount code for your next purchase: DELAY10. Thank you for your patience and understanding."
"""))

cells.append(create_markdown_cell("""#### Prompt 3: Split Shipment Explanation
**Prompt:**
> "Customer Charlie has an order with multiple items. Explain clearly that his smartphone will arrive tomorrow, but the protective case will arrive separately next week. Avoid corporate jargon."

**Sample Output:**
> "Hi Charlie! I wanted to give you a quick update on your recent order. To get your items to you as fast as possible, we’re shipping them in two separate packages. Your new smartphone is scheduled to arrive tomorrow! Your protective case is coming from a different warehouse and will follow next week. You’ll receive tracking numbers for both packages shortly. Enjoy the new phone!"
"""))

cells.append(create_markdown_cell("""#### Prompt 4: Address Change Too Late
**Prompt:**
> "Customer Diana wants to change her shipping address, but order #987 has already been dispatched. Politely inform her it's too late to change it on our end, but suggest she use the carrier's package reroute portal."

**Sample Output:**
> "Hi Diana, thanks for reaching out. I’ve checked your order #987, and it looks like it has already left our facility and is in the hands of the shipping carrier. Because of this, we can no longer change the address from our system. However, you can easily reroute the package to your new address using the carrier’s online portal. I’ve included the tracking link below where you can request this change. Let me know if you need help navigating it!"
"""))

cells.append(create_markdown_cell("""### Category B: Troubleshooting Guides
"""))

cells.append(create_markdown_cell("""#### Prompt 5: Smart Bulb Reset
**Prompt:**
> "Write a step-by-step guide for a customer whose smart bulb won't connect to Wi-Fi. Assume the fix is to factory reset it by turning the light switch on and off 3 times quickly."

**Sample Output:**
> "Hello! I'm sorry to hear your smart bulb isn't connecting to Wi-Fi. Let's try a quick factory reset, which usually resolves this issue:
> 1. Ensure the power switch controlling the bulb is turned ON.
> 2. Quickly flick the switch OFF and ON three times in a row.
> 3. Wait for the bulb to flash rapidly, indicating it has been reset.
> 4. Open our app and attempt the Wi-Fi setup process again.
> If it still doesn't connect, please reply to this email and we'll dig deeper!"
"""))

cells.append(create_markdown_cell("""#### Prompt 6: Black Screen Laptop
**Prompt:**
> "A customer's laptop screen is entirely black when turned on, but the power light is blinking. Provide a troubleshooting flow starting with a hard reset (holding power for 15 seconds)."

**Sample Output:**
> "Hi there, I understand your laptop screen is staying black while the power light blinks. Let's try a hard reset to drain any residual power and restart the system:
> 1. Unplug the laptop from the charger and remove any connected accessories (USB drives, external monitors).
> 2. Press and hold the power button firmly for 15 seconds, then release it.
> 3. Plug the charger back in.
> 4. Press the power button once to turn the laptop on.
> If the screen remains black, please let me know so we can explore repair options."
"""))

cells.append(create_markdown_cell("""#### Prompt 7: Password Sync Delay
**Prompt:**
> "A user is getting a 'Password Incorrect' error despite resetting their password 5 minutes ago. Explain the 15-minute server sync delay clearly and advise them to clear their browser cache."

**Sample Output:**
> "Hello! I understand you're still getting a 'Password Incorrect' error after resetting your password. Our security servers sometimes take up to 15 minutes to fully sync your new password across all platforms. I recommend waiting just a few more minutes. In the meantime, please clear your browser's cache and cookies to ensure your browser isn't remembering the old login data. You should be able to log in shortly!"
"""))

cells.append(create_markdown_cell("""#### Prompt 8: App Storage Issue
**Prompt:**
> "Customer is trying to install our app but getting 'Insufficient Storage' on their phone. Provide 3 quick, actionable tips to free up space."

**Sample Output:**
> "Hi! It looks like your phone needs a little more room before installing our app. Here are 3 quick tips to clear up some space:
> 1. **Delete unused apps:** Review your phone and uninstall any apps you haven't opened in a while.
> 2. **Clear app caches:** Go to your phone's settings and clear the cached data for large apps like social media or browsers.
> 3. **Back up photos/videos:** Offload your heaviest photos and videos to a cloud service (like Google Photos or iCloud) and delete the local copies.
> Once you've freed up about 500MB, the installation should go smoothly!"
"""))


cells.append(create_markdown_cell("""### Category C: Refund Requests
"""))


cells.append(create_markdown_cell("""#### Prompt 9: Swift Refund Approval
**Prompt:**
> "Customer wants a refund for a software subscription they meant to cancel 2 days ago. Our policy allows a full refund within 3 days. Write the approval message, confirming the refund."

**Sample Output:**
> "Hi there, thanks for reaching out. No worries at all about forgetting to cancel! Since you are within our 3-day grace period, I have gone ahead and canceled your subscription immediately and issued a full refund. You should see the funds return to your original payment method within 3-5 business days. If you ever need our software in the future, we’d love to have you back."
"""))

cells.append(create_markdown_cell("""#### Prompt 10: Damaged Item - Requesting Proof
**Prompt:**
> "Customer is requesting a refund for a physical item damaged during shipping. Gently ask them to provide photos of both the damaged item and the shipping box before we can process the refund."

**Sample Output:**
> "Hello, I am so sorry to hear that your item arrived damaged! We definitely want to make this right for you. To process your replacement or refund, and to help us file a claim with the delivery carrier, could you please reply to this email with a few clear photos? We will need a photo of the damaged item itself, as well as a photo of the shipping box it arrived in. As soon as we receive those, I'll get this sorted out for you right away."
"""))

cells.append(create_markdown_cell("""#### Prompt 11: Refund Rejection (Policy Violation)
**Prompt:**
> "A user wants a refund for a digital game played for 10 hours. Our policy strictly denies refunds if play time exceeds 2 hours. Write a firm but polite rejection."

**Sample Output:**
> "Hi there, thank you for reaching out regarding a refund for your recent digital game purchase. I have reviewed your account, and I see that the game has been played for 10 hours. Unfortunately, our refund policy states that we can only issue refunds for titles with less than 2 hours of playtime. Therefore, I am unable to approve your refund request. I apologize for any disappointment this may cause and appreciate your understanding of our store policies."
"""))

cells.append(create_markdown_cell("""## 3. Evaluation Table

Here we evaluate the sample outputs against our framework criteria on a **1–5 scale**.

| # | Prompt Category & Focus | Clarity (1-5) | Accuracy (1-5) | Conciseness (1-5) | Overall Score | Notes/Remarks |
|---|-------------------------|---------------|----------------|-------------------|---------------|---------------|
| 1 | Order Status: Standard | 5 | 5 | 5 | **15/15** | Extremely clear and hits all requested details without fluff. |
| 2 | Order Status: Delay | 5 | 5 | 4 | **14/15** | Empathetic and accurate; slightly lengthy but necessary for tone. |
| 3 | Order Status: Split | 5 | 5 | 5 | **15/15** | Avoids jargon perfectly, sets clear expectations easily. |
| 4 | Order Status: Address | 4 | 5 | 4 | **13/15** | Good alternative given, though could potentially provide a direct link. |
| 5 | Troubleshoot: Bulb Reset | 5 | 5 | 5 | **15/15** | Step-by-step format excels in clarity and brevity. |
| 6 | Troubleshoot: Laptop | 5 | 5 | 5 | **15/15** | Excellent structure and highly accurate sequence of operations. |
| 7 | Troubleshoot: Sync Delay | 4 | 5 | 4 | **13/15** | Accurate, but explaining "server sync" might confuse very non-technical users. |
| 8 | Troubleshoot: Storage | 5 | 5 | 5 | **15/15** | Actionable, easy to execute, perfectly concise. |
| 9 | Refund: Swift Approval | 5 | 5 | 5 | **15/15** | Very reassuring tone, accurate policy enforcement, right to the point. |
| 10| Refund: Damage Proof | 5 | 5 | 4 | **14/15** | Empathetic and clear instructions; slightly wordy but polite. |
| 11| Refund: Rejection | 5 | 5 | 5 | **15/15** | Firm, points strictly to the policy, polite but unambiguous. |
"""))

cells.append(create_markdown_cell("""## 4. Final Report Summary

### Key Findings
1. **The Power of Formatting:** The highest-scoring prompts (particularly in the Troubleshooting category) generated lists and step-by-step instructions. Explicitly asking the AI to "Provide a step-by-step guide" drastically improves **Clarity** and **Conciseness**.
2. **Tone Balancing:** In scenarios requiring apologies (Prompt 2) or rejections (Prompt 11), conciseness occasionally competes with empathy. Allowing slightly longer responses ensures the customer feels heard, even if it brings the *Conciseness* score down slightly.
3. **Addressing Alternatives:** Scenarios where we cannot fulfill the immediate request (Prompt 4, Address Change) require the AI to provide alternative workflows. Formulating prompts to say "Politely inform... but suggest [alternative]" yields highly accurate and helpful outputs.

### Recommendations for Future Prompts
- **Include Formatting Constraints:** Always prompt the AI to use lists for multi-step processes or options.
- **Provide Policy Frameworks within the Prompt:** As seen in the Refund category, giving exact numbers (e.g., "3 days," "2 hours") directly in the prompt prevents AI hallucinations and ensures 100% **Accuracy**.
- **Define Tone Explicitly:** Instructing the AI to be "firm but polite" or "empathetic" effectively steers the language generation away from robotic or overly-casual phrasing.

This library serves as a robust baseline. By iterating on these templates based on this evaluation framework, the support team can consistently deploy high-quality AI responses that improve customer satisfaction.
"""))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open(r'c:\\lakshya documents\\assignment1(day1)\\Customer_Support_Prompt_Library.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Notebook successfully created.")
