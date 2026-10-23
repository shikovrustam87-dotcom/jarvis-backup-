/**
 * Джарвис — переключатель ВИЗУАЛ / ЧАТ.
 * Две строки в боковой панели (рядом с «Сеансы», «Боты»).
 * Клик по строке разворачивает нужное окно на весь экран.
 */
import { cn, haptic, host, Tip } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'jarvis-switch'

function switchTo(which) {
  haptic('tap')
  fetch('/api/plugins/' + ID + '/switch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ target: which })
  })
    .then((r) => r.json())
    .then((d) => {
      host.notify({
        kind: d.ok ? 'info' : 'error',
        message: d.message || (d.ok ? 'Готово' : 'Ошибка')
      })
    })
    .catch((e) => {
      host.notify({ kind: 'error', message: 'Не удалось: ' + e.message })
    })
}

function NavRow({ which, label, hint, codicon }) {
  return jsx(Tip, {
    label: hint,
    children: jsxs('button', {
      type: 'button',
      className: cn(
        'flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-[0.8125rem]',
        'text-(--ui-text-secondary) transition-colors',
        'hover:bg-(--chrome-action-hover) hover:text-foreground'
      ),
      onClick: () => switchTo(which),
      children: [
        jsx('span', {
          className: 'codicon codicon-' + codicon,
          style: { fontSize: '14px' }
        }),
        jsx('span', { children: label })
      ]
    })
  })
}

function JarvisSwitcher() {
  return jsxs('div', {
    className: 'flex flex-col gap-0.5 px-1 py-1',
    children: [
      jsx(NavRow, {
        which: 'visual',
        label: 'Визуал',
        hint: 'Развернуть заставку Джарвиса на весь экран',
        codicon: 'eye'
      }),
      jsx(NavRow, {
        which: 'chat',
        label: 'Чат',
        hint: 'Вернуться к переписке на весь экран',
        codicon: 'comment-discussion'
      })
    ]
  })
}

export default {
  id: ID,
  name: 'Джарвис — переключатель',
  register(ctx) {
    ctx.register({
      id: 'nav',
      area: 'sidebar.nav',
      order: 40,
      render: () => jsx(JarvisSwitcher, {})
    })
  }
}