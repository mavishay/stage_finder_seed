// Components
import type {TemplateResult} from "lit";
import {html} from "lit";
import {customElement, property} from "lit/decorators.js";

import {TwLitElement} from "../common/TwLitElement";

import "../components/HelloWorld";

@customElement("x-index-page")
export class IndexPage extends TwLitElement {
    @property() messages = [{type: "question", data: "What can you do?"}, {type: "answer", data: "All kind of things"}];
    @property() newMessage = ""

    @property() ws = new WebSocket(import.meta.env.VITE_WS_URL as string || "ws://localhost:9090/langchain/ws");

    async firstUpdated() {
        // Give the browser a chance to paint
        await new Promise((r) => setTimeout(r, 0));
        this.ws.addEventListener('message', (event) => {
            try {
                const content = JSON.parse(event.data || "{}")
                this.messages = [...this.messages, content]
            } catch (e) {
                console.warn(e)
            }
        });
    }

    private setNewMessage(event) {
        this.newMessage = event.target.value
    }

    private sendMessage() {
        if (this.newMessage.length === 0) return
        this.ws.send(this.newMessage)
        this.newMessage = '';
    }

    private handleKeyDown(event) {
        if (event.key === 'Enter') {
            this.sendMessage()
        }
    }

  render(): TemplateResult {
    return html`
        <main class="container min-h-screen max-h-screen mx-5 lg:mx-auto py-5 flex flex-col">
            <div class="w-full h-fit grid grid-cols-1 gap-4 lg:grid-cols-2 flex-1 overflow-hidden">
                <div class="w-full flex flex-col items-center justify-center gap-5">
                    <img src="/logo.jpeg"
                         alt="Business index"
                         class="lg-shrink-0 mb-auto lg:-mb-6"
                    />
                    <div class="prose mt-5">
                        <h3 class="text-center">Try asking me something like:</h3>
                        <ul>
                            <li>Give me the data of &quot;Curated AG&quot;</li>
                            <li>What is the address of specific business name</li>
                            <li>Find me 5 business in the video industry</li>
                            <li>And much much more...</li>
                        </ul>
                    </div>
                </div>
                <div
                        class="card bg-base-200 flex-1 rounded-2xl shaddow-2xl p-5 flex justify-between overflow-hidden">
                    <div class="flex-1 overflow-auto pb-5" ref={divRef}>${this.messages?.map((message, index) =>
                            html`
                                <div class="${`chat ${message.type === "question" ? " chat-start" : " chat-end"}`}">
                                    <div
                                            class="${`chat-bubble first-letter ${message.type === "question" ? " chat-bubble-secondary " : " chat-bubble-primary "}`}">
                                        ${message.data}
                                    </div>
                                </div>
                            `
                    )}
                    </div>
                    <label class="input input-bordered flex items-center gap-2 rounded-2xl">
                        <input type="text" class="grow first-letter" placeholder="Type your question here..."
                               value="${this.newMessage}"
                               @keydown=${this.handleKeyDown}
                               @change=${this.setNewMessage}/>
                        <svg @click=${this.sendMessage} xmlns="http://www.w3.org/2000/svg" fill="none"
                             viewBox="0 0 24 24"
                             stroke-width="1.5"
                             stroke="currentColor" class="size-6 cursor-pointer">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                  d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"/>
                        </svg>
                    </label>
                </div>
            </div>
        </main>
    `;
  }
}
