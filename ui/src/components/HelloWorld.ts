import type { TemplateResult } from "lit";
import { html } from "lit";
import { customElement } from "lit/decorators.js";
import { TwLitElement } from "../common/TwLitElement";

@customElement("x-hello-world")
export class HelloWorld extends TwLitElement {
  render(): TemplateResult {
    return html` <button class="chat-bubble">Hello world!</button> `;
  }
}
