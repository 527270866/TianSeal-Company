# Website inquiry delivery

The English, Simplified Chinese, and Spanish inquiry forms are configured to forward submissions to:

**bylandoy1@sklboltseal.com**

They use FormSubmit (`https://formsubmit.co/`) as the static-site form backend.

## One-time activation

1. Publish the website through a web server/hosting provider.
2. Submit one test inquiry from the live website.
3. FormSubmit will send an activation/confirmation email to **bylandoy1@sklboltseal.com**.
4. Open that email and confirm the form.
5. After activation, future inquiries will be forwarded to that inbox.

Form submissions include the visitor's name, business email, selected product, quantity/requirements, and website language. The form also uses FormSubmit's table email template and a hidden honeypot field for spam reduction.

If the recipient address changes later, update the `action` attribute in `index.html`, `zh/index.html`, and `es/index.html`, then activate the new address again.
