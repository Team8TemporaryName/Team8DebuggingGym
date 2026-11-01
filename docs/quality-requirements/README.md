# Quality requirements

The quality requirements the Debugging Gym must meet, and the priority matrix that orders them.
The matrix sorts active records first, then business importance, then technical risk; `QR-nn` order breaks a tie.

| QR | Outcome | Business importance | Technical risk | Characteristic | Sub-characteristic | Status |
| -- | ------- | ------------------- | -------------- | -------------- | ------------------ | ------ |
| [QR-01](qr/QR-01.md) | A learner attaches their own VS Code to a debug runtime within two minutes of starting an exercise. | High | High | Interaction Capability | Operability | Active |
| [QR-02](qr/QR-02.md) | A developer can run the checks that cover the generator and the browser exercise flow from a clean checkout, and a broken change fails them. | High | Medium | Maintainability | Testability | Active |
| [QR-03](qr/QR-03.md) | A debug session that ends mid-run releases its runtime within one minute and keeps no learner code on the server. | High | High | Security | Resistance | Active |
| [QR-04](qr/QR-04.md) | The product stays available for 99.9% of a week once deployed to the production host. | Medium | High | Reliability | Availability | Active |
